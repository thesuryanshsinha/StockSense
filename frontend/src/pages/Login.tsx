import { FormEvent, useState } from "react";
import { Link } from "react-router-dom";
import "./Login.css";

interface LoginFormData {
  email: string;
  password: string;
}

function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] =
    useState<LoginFormData>({
      email: "",
      password: "",
    });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  const handleSubmit = async (
    e: FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:5001/login",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        }
      );

      const data = await response.json();

      console.log("Login response:", data);

      if (!response.ok) {
        throw new Error(
          data.message || "Login failed."
        );
      }

      alert("Login successful!");

      
    } catch (error) {
      console.error("Login error:", error);

      alert(
        error instanceof Error
          ? error.message
          : "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = () => {
    alert(
      "Password reset will be connected to the backend."
    );
  };

  return (
    <div className="login-page">
      {/* LEFT SECTION */}
      <section className="login-intro">
        <div className="intro-brand">
          StockSense
        </div>

        <div className="intro-content">
          <span className="intro-label">
            Welcome Back
          </span>

          <h1>
            Manage your
            <br />
            inventory smarter.
          </h1>

          <p>
            Stay on top of products, stock levels,
            receipts, deliveries, transfers, and
            warehouse operations from one place.
          </p>
        </div>

        <div className="intro-footer">
          Inventory management made simple.
        </div>
      </section>

      {/* RIGHT SECTION */}
      <section className="login-form-section">
        <div className="login-form-container">
          <div className="form-heading">
            <span>Welcome back</span>

            <h2>
              Sign in to StockSense
            </h2>

            <p>
              Enter your details to access your
              inventory workspace.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="login-form"
          >
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

            {/* PASSWORD */}
            <div className="form-group">
              <div className="password-label-row">
                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-button"
                  onClick={handleForgotPassword}
                >
                  Forgot password?
                </button>
              </div>

              <div className="password-wrapper">
                <input
                  id="password"
                  name="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword
                    ? "Hide"
                    : "Show"}
                </button>
              </div>
            </div>

            {/* SUBMIT */}
            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >
              {loading
                ? "Signing in..."
                : "Sign in"}
            </button>
          </form>

          <div className="signup-link">
            Don't have an account?{" "}
            <Link to="/signup">
              Create account
            </Link>
          </div>

          <p className="form-footer">
            Securely access your StockSense
            inventory workspace.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Login;