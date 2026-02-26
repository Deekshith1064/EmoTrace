console.log("🔥 Background service worker started");
let activeTabId = null;
let activeStartTime = null;

/* -----------------------------
   SEND LOG TO BACKEND
----------------------------- */
function sendLogsToBackend(logs) {
  fetch("https://emotrace-backend.onrender.com/log-activity", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(logs)
  })
    .then(response => response.json())
    .then(data => console.log("✅ Logs sent successfully:", data))
    .catch(error => console.error("❌ Error sending logs:", error));
}


/* -----------------------------
   TAB ACTIVATION TRACKING
----------------------------- */
chrome.tabs.onActivated.addListener((activeInfo) => {
  logPreviousTab();
  activeTabId = activeInfo.tabId;
  activeStartTime = Date.now();
});


chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (tabId === activeTabId && changeInfo.status === "complete") {
    activeStartTime = Date.now();
  }
});


/* -----------------------------
   LOG PREVIOUS TAB
----------------------------- */
function logPreviousTab() {

  console.log("📌 logPreviousTab triggered");

  if (activeTabId && activeStartTime) {

    console.log("📌 Valid previous tab found");

    chrome.tabs.get(activeTabId, (tab) => {

      if (!tab.url || tab.url.startsWith("chrome://")) {
        console.log("⛔ Skipping internal tab");
        return;
      }

      const duration = Math.round((Date.now() - activeStartTime) / 1000);

      const log = {
        url: tab.url,
        duration: duration,
        timestamp: new Date().toISOString()
      };

      console.log("🚀 Sending log:", log);

      chrome.storage.local.get(["activityLogs"], (result) => {
        const logs = result.activityLogs || [];
        logs.push(log);

        chrome.storage.local.set({ activityLogs: logs }, () => {
          sendLogsToBackend([log]);
        });
      });

    });
  } else {
    console.log("⚠ No activeTabId or activeStartTime yet");
  }
}

