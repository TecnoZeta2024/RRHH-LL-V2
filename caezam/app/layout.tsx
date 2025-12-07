import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Caezam Protocol - Quantum Ledger",
  description: "Statistical arbitrage platform for lottery optimization",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased">{children}</body>
    </html>
  );
}
