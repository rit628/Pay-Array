'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation';


const LoginPage: React.FC = () => {
    const router = useRouter();
    
    const [formData, setFormData] = useState({
      username: '',
      password: '',
    });
  
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    };
  
    // headers
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      const userData = {
        "username": formData.username,
        "password": formData.password
      };
      const response = await fetch(`${process.env.API_URL}/login/`, {
        "method": "POST",
        "mode": "cors",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": JSON.stringify(userData)
      });
      const header = await response.json();
      localStorage.setItem('auth-header', header);
      
      if (response.ok) {
        router.push("/user");
      }
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
              <button type="submit" className="submit-button">Login</button>
            </form>
          </div>
        </div>
      );
    };
  
  export default LoginPage;