// Firestore data layer for PowerSense.
// Schema:
//   users/{uid}/devices/{deviceId}          -> { name, wattage, hoursPerDay, category, isOn }
//   users/{uid}/settings/general            -> { tariffPerKwh }
//   users/{uid}/predictionHistory/{entryId} -> { timestamp, currentWatts, dailyKwh, monthlyKwh, monthlyBill }
import { db } from "/static/js/firebase-init.js";
import {
  collection, doc, addDoc, updateDoc, deleteDoc, setDoc, getDoc,
  onSnapshot, query, orderBy, limit, serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const DEFAULT_TARIFF = 6.5; // ₹/kWh — matches the Reality module's default rate

// ── Devices ─────────────────────────────────────────────────
export function devicesCol(uid) {
  return collection(db, "users", uid, "devices");
}

export function addDevice(uid, device) {
  return addDoc(devicesCol(uid), {
    name: device.name,
    wattage: Number(device.wattage) || 0,
    hoursPerDay: Number(device.hoursPerDay) || 0,
    category: device.category || "Other",
    isOn: !!device.isOn
  });
}

export function updateDevice(uid, deviceId, patch) {
  return updateDoc(doc(db, "users", uid, "devices", deviceId), patch);
}

export function deleteDevice(uid, deviceId) {
  return deleteDoc(doc(db, "users", uid, "devices", deviceId));
}

// Live-updating list of the user's devices.
export function listenDevices(uid, callback, onError) {
  return onSnapshot(
    devicesCol(uid),
    (snap) => {
      const devices = snap.docs.map(d => ({ id: d.id, ...d.data() }));
      callback(devices);
    },
    (err) => {
      console.error('listenDevices error:', err);
      if (onError) onError(err);
    }
  );
}

// ── Settings (tariff etc.) ─────────────────────────────────
export async function getSettings(uid) {
  const ref = doc(db, "users", uid, "settings", "general");
  const snap = await getDoc(ref);
  if (snap.exists()) return snap.data();
  return { tariffPerKwh: DEFAULT_TARIFF };
}

export function setSettings(uid, settings) {
  return setDoc(doc(db, "users", uid, "settings", "general"), settings, { merge: true });
}

// ── Prediction history (throttled snapshots for trend charts) ─
export function addPredictionSnapshot(uid, snapshot) {
  return addDoc(collection(db, "users", uid, "predictionHistory"), {
    ...snapshot,
    timestamp: serverTimestamp()
  });
}

export function listenRecentPredictionHistory(uid, count, callback) {
  const q = query(
    collection(db, "users", uid, "predictionHistory"),
    orderBy("timestamp", "desc"),
    limit(count)
  );
  return onSnapshot(q, (snap) => {
    const entries = snap.docs.map(d => ({ id: d.id, ...d.data() })).reverse();
    callback(entries);
  });
}
