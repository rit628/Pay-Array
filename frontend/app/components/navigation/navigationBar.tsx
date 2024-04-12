// Navbar.tsx
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="nav">
      <Link href="/" passHref className="site-title">
        PayArray
      </Link>
      <ul>
        <CustomLink href="/home">Home</CustomLink>
        <CustomLink href="/landing">Landing</CustomLink>
        <CustomLink href="/profile">Profile</CustomLink>
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
