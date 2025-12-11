// Simple validation helpers for Day 3

export function validateProduct(name, category, quantity, price) {
    if (!name.trim()) return "Name is required";
    if (!category.trim()) return "Category is required";
    if (isNaN(quantity) || quantity < 0) return "Quantity cannot be negative";
    if (isNaN(price) || price < 0) return "Price cannot be negative";
    return null; // OK
}

export function escapeHtml(s){
  return (s + "").replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
}
