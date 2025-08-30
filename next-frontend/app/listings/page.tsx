"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";


// Simple type for postings
type Posting = { id: number; user: string; car: string; comment: string };

export default function ListingsPage() {
    const router = useRouter();
    const [buyerPosts, setBuyerPosts] = useState<Posting[]>([
        { id: 1, user: "Alice", car: "Toyota RAV4", comment: "Looking for AWD SUV under $30k" },
        { id: 2, user: "Bob", car: "Honda Civic", comment: "Need reliable commuter car" },
    ]);
    const [sellerPosts, setSellerPosts] = useState<Posting[]>([
        { id: 1, user: "Carol", car: "Toyota Camry", comment: "Selling 2020 Camry, 30k miles" },
        { id: 2, user: "Dave", car: "Subaru Forester", comment: "2019 Forester, great condition" },
    ]);

    const handleNewBuyerPost = async () => {
        // Placeholder: call Flowglad to pay $2 before posting
        alert("Here you would charge $2 via Flowglad for a new posting");
    };

    const handleNewSellerPost = async () => {
        alert("Here you would charge $2 via Flowglad for a new posting");
    };

    return (
        <main className="flex h-screen">
        <button
            className="mb-4 px-4 py-2 rounded border"
            onClick={() => router.push("/")}
            >
                ← Back
        </button>
        {/* Left column: Buyer posts */}
        <div className="w-1/2 border-r p-4 overflow-auto">
            <h2 className="text-xl font-bold mb-4">Buyers</h2>
            {buyerPosts.map((p) => (
            <div key={p.id} className="border p-2 mb-2 rounded shadow">
                <strong>{p.user}</strong>: {p.car}
                <p>{p.comment}</p>
            </div>
            ))}
            <button
            onClick={handleNewBuyerPost}
            className="mt-4 bg-green-500 text-white px-3 py-1 rounded"
            >
            Add Buyer Post ($2)
            </button>
        </div>

        {/* Right column: Seller posts */}
        <div className="w-1/2 p-4 overflow-auto">
            <h2 className="text-xl font-bold mb-4">Sellers</h2>
            {sellerPosts.map((p) => (
            <div key={p.id} className="border p-2 mb-2 rounded shadow">
                <strong>{p.user}</strong>: {p.car}
                <p>{p.comment}</p>
            </div>
            ))}
            <button
            onClick={handleNewSellerPost}
            className="mt-4 bg-blue-500 text-white px-3 py-1 rounded"
            >
            Add Seller Post ($2)
            </button>
        </div>
        </main>
    );
}
