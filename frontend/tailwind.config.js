export default {
    content: ["./index.html", "./src/**/*.{ts,tsx}"],
    theme: {
        extend: {
            colors: {
                bg: "#0b1020",
                panel: "#121a2f",
                border: "#273251",
                accent: "#6aa8ff",
                success: "#28c76f",
                pending: "#f59e0b",
            },
            boxShadow: {
                card: "0 0 0 1px rgba(106,168,255,0.15), 0 12px 40px rgba(0,0,0,0.35)",
            },
        },
    },
    plugins: [],
};
