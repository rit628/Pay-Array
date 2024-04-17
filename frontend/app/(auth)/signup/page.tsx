'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation';

const SignUpPage: React.FC = () => {
    const router = useRouter();

    const [formData, setFormData] = useState({
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    });
  
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    };
  
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      console.log(formData);
      if (formData.password === formData.confirmPassword) {
        const userData = {
          "email": formData.email,
          "username": formData.username,
          "password": formData.password
        };
        let response = await fetch(`${process.env.API_URL}/users/`, {
          "method": "POST",
          "mode": "cors",
          "headers": {
            "Content-Type": "application/json"
          },
          "body": JSON.stringify(userData)
        })

        let data = await response.json();
        console.log(data);
        if (!response.ok) {
          return;
        }
        response = await fetch(`${process.env.API_URL}/login/`, {
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
          router.push("/joinhouse");
        }
      }
    };
  
    return (
      <>
      <title>Sign Up | PayArray</title>
        <div className="container">
          <div className="login-container">
            <h2 className="title">Sign Up</h2>
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="email" className="label">
                  Email:
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your email"
                  required
                />
              </div>
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
              <div className="form-group">
                <label htmlFor="confirmPassword" className="label">
                  Confirm Password:
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="input"
                  placeholder="Confirm your password"
                  required
                />
              </div>
              <Link href='/joinhouse'>
              <button type="submit" className="submit-button">Sign Up</button>
              </Link>
            </form>
          </div>
        </div>
        </>
      );
    };
  
  export default SignUpPage;