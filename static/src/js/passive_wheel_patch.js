(function () {
    'use strict';
    // Small shim to default certain scroll-related event listeners to passive
    // to avoid '[Violation] Added non-passive event listener to a scroll-blocking' warnings.
    // This monkey-patches addEventListener for the specific event types only.
    const origAddEventListener = EventTarget.prototype.addEventListener;

    EventTarget.prototype.addEventListener = function (type, listener, options) {
        try {
            if ((type === 'mousewheel' || type === 'wheel' || type === 'touchstart' || type === 'touchmove') && (options === undefined || options === null)) {
                // Prefer passive listeners for scroll/touch events to improve responsiveness
                return origAddEventListener.call(this, type, listener, { passive: true });
            }
        } catch (err) {
            // If anything goes wrong, fall back to original behavior
        }
        return origAddEventListener.call(this, type, listener, options);
    };
})();
