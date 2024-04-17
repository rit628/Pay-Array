'use client'
import { useState } from 'react'
import Link from 'next/link';


const LoginPage: React.FC = () => {
    const [formData, setFormData] = useState({
      username: '',
      password: '',
    });
  
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    };
  
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      console.log(formData);
      // logic
    };
  
    return (
        <div className="container">
          <div className="login-container">
            <h2 className="title">Login</h2>
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="username" className="label">
                  Username:
                </label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password" className="label">
                  Password:
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <Link href="/userPage">
              <button type="submit" className="submit-button">Login</button>
              </Link>
            </form>
          </div>
        </div>
      );
    };
  
  export default LoginPage;