self.addEventListener("push", function(event) {
    const data = event.data.json();
    self.registration.showNotification(data.head, {
        body: data.body,
        icon: data.icon,
        data: { url: data.url }
    });
});

self.addEventListener("notificationclick", function(event) {
    event.notification.close();
    event.waitUntil(clients.openWindow(event.notification.data.url));
});
