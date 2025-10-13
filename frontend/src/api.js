import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

// ✅ Fetch all products
export const getProducts = async () => {
  const res = await axios.get(`${API_BASE}/products/`);
  return res.data;
};

// ✅ Fetch recommendations for a given product
export const getRecommendations = async (id) => {
  const res = await axios.get(`${API_BASE}/products/${id}/recommendations`);
  return res.data;
};
