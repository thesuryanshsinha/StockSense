import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// Authentication pages
import Login from "./pages/Login";
import Signup from "./pages/Signup";

// Dashboards
import ManagerDashboard from "./pages/ManagerDashboard";
import WarehouseDashboard from "./pages/WarehouseDashboard";

// Other pages
import Products from "./pages/Products";
import Receipts from "./pages/Receipts";
import Deliveries from "./pages/Deliveries";
import Transfers from "./pages/Transfers";
import Adjustments from "./pages/Adjustments";
import MoveHistory from "./pages/MoveHistory";
import Warehouse from "./pages/Warehouse";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default route */}
        <Route
          path="/"
          element={<Navigate to="/login" replace />}
        />

        {/* Authentication */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Manager */}
        <Route
          path="/manager/dashboard"
          element={<ManagerDashboard />}
        />

        {/* Warehouse Staff */}
        <Route
          path="/warehouse/dashboard"
          element={<WarehouseDashboard />}
        />

        {/* Inventory Management */}
        <Route path="/products" element={<Products />} />
        <Route path="/receipts" element={<Receipts />} />
        <Route path="/deliveries" element={<Deliveries />} />
        <Route path="/transfers" element={<Transfers />} />
        <Route path="/adjustments" element={<Adjustments />} />
        <Route path="/move-history" element={<MoveHistory />} />

        {/* Warehouse */}
        <Route path="/warehouse" element={<Warehouse />} />

        {/* User */}
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />

        {/* Unknown route */}
        <Route
          path="*"
          element={<Navigate to="/login" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;