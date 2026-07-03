// Pure calculation engine for the Prediction module's virtual household.
// No Firebase/DOM dependencies — same logic can run on prediction.html
// (to drive the live simulation) and compare.html (to compute the
// "predicted" side of the comparison) without duplicating formulas.

// Instantaneous simulated power draw right now, from devices toggled ON.
// Small jitter mimics real sensor noise, same spirit as the Reality module.
export function currentWatts(devices) {
  return devices
    .filter(d => d.isOn)
    .reduce((sum, d) => sum + d.wattage * (0.92 + Math.random() * 0.16), 0);
}

// Projected consumption based on each device's configured wattage and
// average hours/day — independent of live ON/OFF state, since that
// reflects planned usage rather than this instant's switch position.
export function computeSnapshot(devices, tariffPerKwh) {
  const dailyWh = devices.reduce((sum, d) => sum + d.wattage * (d.hoursPerDay || 0), 0);
  const dailyKwh = dailyWh / 1000;
  const weeklyKwh = dailyKwh * 7;
  const monthlyKwh = dailyKwh * 30;

  const dailyBill = dailyKwh * tariffPerKwh;
  const weeklyBill = weeklyKwh * tariffPerKwh;
  const monthlyBill = monthlyKwh * tariffPerKwh;

  const contributions = devices
    .map(d => ({
      id: d.id,
      name: d.name,
      category: d.category,
      watts: d.wattage,
      isOn: d.isOn,
      dailyKwh: (d.wattage * (d.hoursPerDay || 0)) / 1000
    }))
    .sort((a, b) => b.dailyKwh - a.dailyKwh);

  const highest = contributions.length ? contributions[0] : null;
  const lowest = contributions.length ? contributions[contributions.length - 1] : null;

  return {
    currentWatts: currentWatts(devices),
    dailyKwh, weeklyKwh, monthlyKwh,
    dailyBill, weeklyBill, monthlyBill,
    contributions, highest, lowest
  };
}
