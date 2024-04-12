// Navbar.tsx
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="nav">
      <Link href="/" passHref>
        <a className="site-title">Site Name</a>
      </Link>
      <ul>
        <CustomLink href="/home">Pricing</CustomLink>
        <CustomLink href="/landing">About</CustomLink>
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
      <Link href={href}>{children}</Link>
    </li>
  );
}
