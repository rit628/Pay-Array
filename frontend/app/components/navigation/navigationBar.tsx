'use client'
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();
  const handleLogout = () => {
    localStorage.clear();
    router.push("/");
  }
  return (
    <nav className="nav">
      <Link href="/" passHref className="site-title">
        PayArray
      </Link>
      <ul>
        <CustomLink href="/household">Household</CustomLink>
        <CustomLink href="/user">User</CustomLink>
        <button onClick={handleLogout}>Logout</button>
      </ul>
    </nav>
  );
}

interface CustomLinkProps {
  href: string;
  children: React.ReactNode;
}

function CustomLink({ href, children }: CustomLinkProps) {
  return (
    <li>
      <Link href={href} legacyBehavior>{children}</Link>
    </li>
  );
}
