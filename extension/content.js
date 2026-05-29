if (window.aiModeratorLoaded) {
    console.log("Already running, skipping...");
} else {
    window.aiModeratorLoaded = true;

    console.log(" AI EXTENSION LOADED ");

    async function checkText(element) {

        let text = element.innerText;

        // Filters
        if (!text || text.length < 10) return;
        if (text.length > 300) return;
        if (text.split(" ").length < 3) return;


        const toxicKeywords = [
            "fuck", "fucking", "shit", "bitch", "asshole",
            "racist", "hate", "kill", "die", "stupid",
            "idiot", "dumb", "moron"
        ];

        let lowerText = text.toLowerCase();
        let keywordToxic = toxicKeywords.some(word => lowerText.includes(word));

        let parent = element.closest('[data-testid="comment"]') || element.closest("div");

        if (!parent) return;

        if (parent.dataset.checked) return;
        parent.dataset.checked = "true";

        try {
            let response = await fetch("https://ai-content-moderation-5kkf.onrender.com/moderate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });

            let data = await response.json();

            if (data.result === "Toxic" || keywordToxic) {

                parent.style.filter = "blur(6px) brightness(0.7)";
                parent.style.transition = "0.3s";
                parent.style.cursor = "pointer";
                parent.style.padding = "5px";
                parent.style.backgroundColor = "rgba(255,0,0,0.15)";

                if (!parent.dataset.warned) {
                    parent.dataset.warned = "true";

                    let warning = document.createElement("div");
                    warning.innerText = "⚠️ Toxic content (click to view)";
                    warning.style.color = "red";
                    warning.style.fontSize = "12px";
                    warning.style.marginBottom = "5px";
                    warning.style.fontWeight = "bold";

                    parent.insertBefore(warning, parent.firstChild);
                }

                parent.addEventListener("click", () => {
                    parent.style.filter = "none";
                    parent.style.backgroundColor = "transparent";
                });
            }

        } catch (error) {
            console.log("API error:", error);
        }
    }

    function scanPage() {
        document.querySelectorAll("p, h1, h2, h3, span").forEach(el => {
            checkText(el);
        });
    }

    scanPage();

    let timeout;

    const observer = new MutationObserver(() => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            scanPage();
        }, 500);
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    let lastUrl = location.href;

    new MutationObserver(() => {
        const url = location.href;

        if (url !== lastUrl) {
            lastUrl = url;
            console.log(" Page changed, re-running moderation...");
            scanPage();
        }
    }).observe(document, { subtree: true, childList: true });
}