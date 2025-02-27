import type { Metadata } from "next";
import styles from '@styles/background.module.css';
import { Lexend } from "next/font/google";
import "./styles/globals.css";

const lexend = Lexend({
  variable: "--font-lexend",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Monitoreo de Cambios de Interfaces",
  icons: {
    icon: '/logo.png'
  }
};

export default function RootLayout({ children, }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en">
      <body className={`${styles.gradient} ${lexend.variable} antialiased min-w-fit`}>
        {children}
      </body>
    </html>
  );
}
