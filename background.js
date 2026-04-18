// Listen for the extension installation event
chrome.runtime.onInstalled.addListener(() => {
  console.log("✅ Privacy Checker Extension installed successfully.");
});

// Placeholder for future background tasks
// Example: Listening for messages from the popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "log") {
    console.log("📩 Message received from content script or popup:", message.data);
    sendResponse({ status: "Message logged successfully" });
  }
});