import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Signup.css";

type UserRole = "manager" | "warehouse";

interface SignupFormData {
  fullName: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: UserRole;
}

function Signup() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState<SignupFormData>({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "warehouse",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Check passwords
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    // Basic password validation
    if (formData.password.length < 8) {
      alert("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:5001/register",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            fullName: formData.fullName,
            email: formData.email,
            password: formData.password,
            role: formData.role,
          }),
        }
      );

      const data = await response.json();

      console.log("Signup response:", data);

      if (!response.ok) {
        throw new Error(data.message || "Signup failed.");
      }

      alert("Account created successfully!");

      // Go to login after successful signup
      navigate("/login");
    } catch (error) {
      console.error("Signup error:", error);

      alert(
        error instanceof Error
          ? error.message
          : "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page">
      {/* LEFT SECTION */}
      <section className="signup-intro">
        <div className="intro-brand">StockSense</div>

        <div className="intro-content">
          <span className="intro-label">Get Started</span>

          <h1>
            Take control
            <br />
            of your inventory.
          </h1>

          <p>
            Create your StockSense account to manage products,
            stock movements, receipts, deliveries, and warehouse
            operations from one place.
          </p>
        </div>

        <div className="intro-footer">
          Inventory management made simple.
        </div>
      </section>

      {/* RIGHT SECTION */}
      <section className="signup-form-section">
        <div className="signup-form-container">
          <div className="form-heading">
            <span>Create your account</span>

            <h2>Join StockSense</h2>

            <p>Create your account to get started.</p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="signup-form"
          >
            {/* FULL NAME */}
            <div className="form-group">
              <label htmlFor="fullName">
                Full name
              </label>

              <input
                id="fullName"
                name="fullName"
                type="text"
                placeholder="Your name"
                value={formData.fullName}
                onChange={handleChange}
                required
              />
            </div>

            {/* EMAIL */}
            <div className="form-group">
              <label htmlFor="email">
                Email address
              </label>

              <input
                id="email"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            {/* ROLE */}
            <div className="form-group">
              <label htmlFor="role">
                Account type
              </label>

              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                required
              >
                <option value="staff">
                  Warehouse Staff
                </option>

                <option value="manager">
                  Inventory Manager
                </option>
              </select>
            </div>

            {/* PASSWORD */}
            <div className="form-group">
              <label htmlFor="password">
                Password
              </label>

              <div className="password-wrapper">
                <input
                  id="password"
                  name="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="At least 8 characters"
                  value={formData.password}
                  onChange={handleChange}
                  minLength={8}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* CONFIRM PASSWORD */}
            <div className="form-group">
              <label htmlFor="confirmPassword">
                Confirm password
              </label>

              <div className="password-wrapper">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={
                    showConfirmPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password again"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  minLength={8}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowConfirmPassword(
                      !showConfirmPassword
                    )
                  }
                >
                  {showConfirmPassword
                    ? "Hide"
                    : "Show"}
                </button>
              </div>
            </div>

            {/* SUBMIT */}
            <button
              type="submit"
              className="signup-button"
              disabled={loading}
            >
              {loading
                ? "Creating account..."
                : "Create account"}
            </button>
          </form>

          <div className="login-link">
            Already have an account?{" "}
            <Link to="/login">
              Sign in
            </Link>
          </div>

          <p className="form-footer">
            StockSense helps businesses organize
            inventory, warehouse operations, and stock
            movement in one place.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Signup;