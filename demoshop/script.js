let total = 0;
const totalSpan = document.getElementById("total");
const productsContainer = document.getElementById("productsContainer");
const buyedList = document.getElementById("buyedList");
let products = [];
let buyed = [];

// Update total display
function updateTotal() {
  totalSpan.textContent = total.toFixed(2);
}

// Update buyed products display, grouping duplicates
function updateBuyedList() {
  buyedList.innerHTML = '';

  // Count quantities
  const grouped = {};
  buyed.forEach(item => {
    if (grouped[item.name]) {
      grouped[item.name].qty += 1;
      grouped[item.name].total += item.p;
    } else {
      grouped[item.name] = { qty: 1, total: item.p, price: item.p };
    }
  });

  // Render list
  for (const name in grouped) {
    const li = document.createElement('li');
    const item = grouped[name];
    li.textContent = `${name} x${item.qty} - $${item.total.toFixed(2)}`;
    buyedList.appendChild(li);
  }
}

// Load products dynamically
fetch('Products.json')
  .then(r => r.json())
  .then(data => {
    products = data;

    products.forEach((prod, index) => {
      const card = document.createElement('div');
      card.className = 'item-card';
      
      card.innerHTML = `
        <h2>${prod.name}</h2>
        <p>$${prod.p}</p>
        <button class="buyBtn" data-index="${index}">Buy ${prod.name}</button>
      `;
      productsContainer.appendChild(card);
    });

    // Attach click events to buy buttons
    document.querySelectorAll('.buyBtn').forEach(btn => {
      btn.addEventListener('click', () => {
        const index = parseInt(btn.dataset.index);
        const product = products[index];

        // Update total
        total += product.p;
        updateTotal();

        // Add to buyed array
        buyed.push(product);
        updateBuyedList();

        // Update buyed.json (works only with server)
        fetch('buyed.json', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(buyed, null, 2)
        }).catch(() => console.warn('Cannot write buyed.json without server.'));
      });
    });
  })
  .catch(err => console.error('Error loading Products.json:', err));

// Initialize displays
updateTotal();
updateBuyedList();
