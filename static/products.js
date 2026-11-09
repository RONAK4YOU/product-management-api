const api = "/products";
const byId = (id) => document.getElementById(id);

function showMessage(message, isError = false) {
  const el = byId("flash_message");
  el.textContent = message;
  el.style.color = isError ? "#a92b36" : "#176b3a";
}

function renderProducts(products) {
  byId("search_results").innerHTML = products.map((p) => `
    <article class="product">
      <strong>${escapeHtml(p.name)}</strong> — ${escapeHtml(p.description)}
      <div>ID: <code>${p.id}</code> · Category: ${escapeHtml(p.category)} · Price: ${p.price} · Available: ${p.available}</div>
    </article>`).join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}

async function searchProducts() {
  const params = new URLSearchParams();
  if (byId("search_name").value.trim()) params.set("name", byId("search_name").value.trim());
  if (byId("search_category").value.trim()) params.set("category", byId("search_category").value.trim());
  if (byId("search_available").value) params.set("available", byId("search_available").value);
  try {
    const response = await fetch(`${api}?${params}`);
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "Search failed");
    renderProducts(body.products);
    showMessage("Success");
  } catch (error) { showMessage(error.message, true); }
}

function clearForm() {
  ["search_name", "search_category"].forEach((id) => { byId(id).value = ""; });
  byId("search_available").value = "";
  byId("search_results").replaceChildren();
  byId("product_details").replaceChildren();
  byId("product_id").value = "";
  showMessage("");
}

async function createProduct() {
  const payload = {
    name: byId("name").value,
    description: byId("description").value,
    price: Number(byId("price").value),
    available: byId("available").value === "true",
    category: byId("category").value,
  };
  const response = await fetch(api, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) });
  const body = await response.json();
  showMessage(response.ok ? "Product created" : body.error, !response.ok);
  if (response.ok) byId("product_id").value = body.id;
}

async function retrieveProduct() {
  const response = await fetch(`${api}/${byId("product_id").value}`);
  const body = await response.json();
  if (!response.ok) { showMessage(body.error, true); return; }
  byId("product_details").textContent = `Name: ${body.name} | Description: ${body.description} | Availability: ${body.available} | Category: ${body.category} | Price: ${body.price}`;
  showMessage("Success");
}

async function updateProduct() {
  const productId = byId("product_id").value;
  const response = await fetch(`${api}/${productId}`, { method: "PUT", headers: {"Content-Type":"application/json"}, body: JSON.stringify({ name: byId("name").value, description: byId("description").value, price: Number(byId("price").value), available: byId("available").value === "true", category: byId("category").value }) });
  const body = await response.json();
  showMessage(response.ok ? "Product updated" : body.error, !response.ok);
}

async function deleteProduct() {
  const response = await fetch(`${api}/${byId("product_id").value}`, { method: "DELETE" });
  if (response.status === 204) { byId("product_details").replaceChildren(); showMessage("Product deleted"); }
  else { const body = await response.json(); showMessage(body.error, true); }
}
