/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        API_URL: process.env.API_URL,
        AUTH_TYPE : process.env.AUTH_TYPE
    }
};

export default nextConfig;
