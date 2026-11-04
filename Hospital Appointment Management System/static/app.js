const state = { patients: [], doctors: [], appointments: [] };
const $ = (selector, root = document) => root.querySelector(selector);
const escapeHtml = (value = "") => String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
let toastTimer;

function notify(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}

async function request(url, method = "GET", body) {
  const response = await fetch(url, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Something went wrong.");
  if (result.data) render(result.data);
  return result;
}

function render(data) {
  Object.assign(state, data);
  $("#patient-count").textContent = state.patients.length;
  $("#doctor-count").textContent = state.doctors.length;
  $("#appointment-count").textContent = state.appointments.length;
  renderPatients();
  renderDoctors();
  renderAppointments();
  fillSelects();
}

function personCell(name, subtitle, initials) {
  return `<div class="person"><span class="person-badge">${escapeHtml(initials)}</span><span><span class="person-name">${escapeHtml(name)}</span>${subtitle ? `<span class="person-sub">${escapeHtml(subtitle)}</span>` : ""}</span></div>`;
}

function renderPatients() {
  $("#patients-table").innerHTML = state.patients.map(patient => `<tr>
    <td>${personCell(patient.name, `Patient #${patient.id}`, patient.name.trim().split(/\s+/).map(part => part[0]).join("").slice(0, 2).toUpperCase())}</td>
    <td>${escapeHtml(patient.phone)}</td><td>${escapeHtml(patient.email || "—")}</td>
    <td><div class="row-actions"><button class="small-btn" data-action="edit-patient" data-id="${patient.id}">Edit</button><button class="small-btn danger" data-action="delete-patient" data-id="${patient.id}">Delete</button></div></td></tr>`).join("");
  $("#patients-empty").classList.toggle("hidden", state.patients.length > 0);
}

function renderDoctors() {
  $("#doctors-table").innerHTML = state.doctors.map(doctor => `<tr>
    <td>${personCell(`Dr. ${doctor.name}`, `Doctor #${doctor.id}`, doctor.name.trim().split(/\s+/).map(part => part[0]).join("").slice(0, 2).toUpperCase())}</td>
    <td><span class="specialty">${escapeHtml(doctor.specialty)}</span></td><td>${escapeHtml(doctor.phone || "—")}</td>
    <td><div class="row-actions"><button class="small-btn" data-action="edit-doctor" data-id="${doctor.id}">Edit</button><button class="small-btn danger" data-action="delete-doctor" data-id="${doctor.id}">Delete</button></div></td></tr>`).join("");
  $("#doctors-empty").classList.toggle("hidden", state.doctors.length > 0);
}

function renderAppointments() {
  $("#appointments-table").innerHTML = state.appointments.map(item => {
    const dateLabel = new Date(`${item.date}T00:00:00`).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
    return `<tr><td>${personCell(item.patient_name, `Patient #${item.patient_id}`, item.patient_name.trim().split(/\s+/).map(part => part[0]).join("").slice(0, 2).toUpperCase())}</td>
    <td>${personCell(`Dr. ${item.doctor_name}`, item.doctor_specialty, item.doctor_name.trim().split(/\s+/).map(part => part[0]).join("").slice(0, 2).toUpperCase())}</td>
    <td>${escapeHtml(dateLabel)}<span class="person-sub">${escapeHtml(item.time)}</span></td><td>${escapeHtml(item.reason || "—")}</td>
    <td><div class="row-actions"><button class="small-btn" data-action="edit-appointment" data-id="${item.id}">Edit</button><button class="small-btn danger" data-action="delete-appointment" data-id="${item.id}">Cancel</button></div></td></tr>`;
  }).join("");
  $("#appointments-empty").classList.toggle("hidden", state.appointments.length > 0);
}

function fillSelects() {
  const patientSelect = $('#appointment-form [name="patient_id"]');
  const doctorSelect = $('#appointment-form [name="doctor_id"]');
  const previousPatient = patientSelect.value;
  const previousDoctor = doctorSelect.value;
  patientSelect.innerHTML = `<option value="">Choose a patient</option>` + state.patients.map(item => `<option value="${item.id}">${escapeHtml(item.name)}</option>`).join("");
  doctorSelect.innerHTML = `<option value="">Choose a doctor</option>` + state.doctors.map(item => `<option value="${item.id}">Dr. ${escapeHtml(item.name)} · ${escapeHtml(item.specialty)}</option>`).join("");
  if (previousPatient) patientSelect.value = previousPatient;
  if (previousDoctor) doctorSelect.value = previousDoctor;
}

function openForm(kind, record) {
  const card = $(`#${kind}-form-card`);
  const form = $(`#${kind}-form`);
  form.reset();
  form.elements.record_id.value = record?.id || "";
  if (kind === "appointment") {
    $("#appointment-form-title").textContent = record ? "Edit appointment" : "Schedule an appointment";
    if (record) for (const key of ["patient_id", "doctor_id", "date", "time", "reason"]) form.elements[key].value = record[key] ?? "";
  } else {
    $(`#${kind}-form-title`).textContent = `${record ? "Edit" : "Add a"} ${kind}`;
    if (record) for (const key of Object.keys(record)) if (form.elements[key]) form.elements[key].value = record[key] ?? "";
  }
  card.classList.remove("hidden");
  card.scrollIntoView({ behavior: "smooth", block: "center" });
}

function closeForms() { document.querySelectorAll(".form-card").forEach(card => card.classList.add("hidden")); }

function formData(form, fields) {
  const data = {};
  for (const key of fields) data[key] = form.elements[key].value.trim();
  return data;
}

function showError(error) { notify(error.message); }

$("#today-label").textContent = new Date().toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
document.querySelectorAll(".tab").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(tab => tab.classList.toggle("active", tab === button));
  document.querySelectorAll(".panel").forEach(panel => panel.classList.toggle("active", panel.id === `panel-${button.dataset.tab}`));
  closeForms();
}));

$("#new-appointment-button").addEventListener("click", () => openForm("appointment"));
$("#empty-new-appointment").addEventListener("click", () => openForm("appointment"));
$("#new-patient-button").addEventListener("click", () => openForm("patient"));
$("#new-doctor-button").addEventListener("click", () => openForm("doctor"));
document.querySelectorAll(".close-form").forEach(button => button.addEventListener("click", closeForms));

$("#patient-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const id = form.elements.record_id.value;
  try { await request(id ? `/api/patients/${id}` : "/api/patients", id ? "PUT" : "POST", formData(form, ["name", "phone", "email"])); closeForms(); notify(id ? "Patient updated." : "Patient added."); }
  catch (error) { showError(error); }
});

$("#doctor-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const id = form.elements.record_id.value;
  try { await request(id ? `/api/doctors/${id}` : "/api/doctors", id ? "PUT" : "POST", formData(form, ["name", "specialty", "phone"])); closeForms(); notify(id ? "Doctor updated." : "Doctor added."); }
  catch (error) { showError(error); }
});

$("#appointment-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const id = form.elements.record_id.value;
  const payload = formData(form, ["patient_id", "doctor_id", "date", "time", "reason"]);
  try { await request(id ? `/api/appointments/${id}` : "/api/appointments", id ? "PUT" : "POST", payload); closeForms(); notify(id ? "Appointment updated." : "Appointment scheduled."); }
  catch (error) { showError(error); }
});

document.addEventListener("click", async event => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const id = Number(button.dataset.id);
  const action = button.dataset.action;
  const [operation, type] = action.split("-");
  const collection = type === "appointment" ? "appointments" : `${type}s`;
  if (operation === "edit") {
    const record = state[collection].find(item => item.id === id);
    document.querySelector(`.tab[data-tab="${collection}"]`).click();
    openForm(type, record);
    return;
  }
  const label = type === "appointment" ? "appointment" : type;
  if (!confirm(`${operation === "delete" && type === "appointment" ? "Cancel" : "Delete"} this ${label}?`)) return;
  try { await request(`/api/${collection}/${id}`, "DELETE"); notify(type === "appointment" ? "Appointment cancelled." : `${type[0].toUpperCase()}${type.slice(1)} deleted.`); }
  catch (error) { showError(error); }
});

request("/api/data").catch(showError);
