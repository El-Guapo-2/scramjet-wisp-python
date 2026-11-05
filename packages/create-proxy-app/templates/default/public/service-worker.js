const originalFetch = globalThis.fetch.bind(globalThis);
globalThis.fetch = async (input, init) => {
	const response = await originalFetch(input, init);
	const url = typeof input === "string" ? input : input.url;
	if (url.endsWith("/package.json") &&
		url.includes("@mercuryworkshop/scramjet-controller@")) {
		const packageJson = await response.json();
		packageJson.dependencies = {
			...(packageJson.dependencies || {}),
			"@mercuryworkshop/scramjet": "2.0.67-alpha.2",
		};
		return new Response(JSON.stringify(packageJson), {
			status: response.status,
			headers: response.headers,
		});
	}
	return response;
};

importScripts(
	"https://cdn.jsdelivr.net/npm/@mercuryworkshop/proxy-bootstrap@0.0.5/dist/bootstrap-static.js"
);

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => {
	event.waitUntil(self.clients.claim());
});
