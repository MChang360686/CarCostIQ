"use client";
import { useRouter } from "next/navigation";

export default function Help() {
    const router = useRouter();

    return (
    <main className="mx-auto max-w-3xl p-6">
        <button
        className="mb-4 px-4 py-2 rounded border"
        onClick={() => router.push("/")}
        >
            ← Back
        </button>
      <h1 className="text-2xl font-bold mb-4">FAQ</h1>
        <h2 className="text-xl font-semibold mb-2">How does this work?</h2>
        <p>This tool uses AI to analyze your situation and recommend cars and insurance options based on your input.</p>
        <h2 className="text-xl font-semibold mb-2">Can I trust the results?</h2>    
        <p>Yes, the results are based on the information you provide and are provided by a trusted third-party.
        However, always do your own research before making any decisions.  Additionally, if you are unsatisfied
        with the available data, you may always post a listing on either our buy or sell pages.
        </p>
        <h2 className="text-xl font-semibold mb-2">How can I contact support?</h2>  
        <p>Email: support@example.com</p>
        <p>Phone: 1-800-123-4567</p>
    </main>
    );
}