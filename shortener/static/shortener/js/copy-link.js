
const copyButton = document.getElementById("copy-button");
const shortLink = document.getElementById("short-link");
const copyMessage = document.getElementById("copy-message");

if (copyButton && shortLink && copyMessage) {
    copyButton.addEventListener("click", async () => {
        try {
            // Copy the complete short URL to the clipboard.
            await navigator.clipboard.writeText(shortLink.href);
            copyMessage.textContent = "Link copied successfully.";
        } catch (error) {
            // Inform the user if clipboard access is unavailable.
            copyMessage.textContent =
                "Unable to copy the link. Please copy it manually.";
        }
    });
}
