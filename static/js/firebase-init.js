// Firebase project init — PowerSense
// These keys identify your Firebase project; they are safe to expose in
// frontend code. Actual security comes from Firestore/Auth rules.
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyA1Qit3t_8evJo1mIldLvQLzEmcK7YW5MI",
  authDomain: "powersense-project.firebaseapp.com",
  projectId: "powersense-project",
  storageBucket: "powersense-project.firebasestorage.app",
  messagingSenderId: "16672831966",
  appId: "1:16672831966:web:665a5568484d38ccae454f"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
