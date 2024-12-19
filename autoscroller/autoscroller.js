let is_scrolling = false;
let start_y = 0;
let scroll_speed = 0;

let arrow;

function setup_autoscroller() {
  // in order to use this you must have an element with the following id
  arrow = document.getElementById('autoscroll-arrow');

  // Toggle autoscrolling on middle mouse click
  document.addEventListener('mousedown', (e) => {
    if (e.button === 1) { // Middle mouse button
      e.preventDefault();
      is_scrolling = !is_scrolling;

      if (is_scrolling) {
        // Activate scrolling
        start_y = e.clientY;
        scroll_speed = 0;
        arrow.style.display = 'block';
        arrow.style.left = `${e.clientX}px`;
        arrow.style.top = `${e.clientY}px`;
        arrow.style.height = '0px';
      } else {
        // Deactivate scrolling
        arrow.style.display = 'none';
      }
    }
  });

  // Adjust scroll speed on mouse movement
  document.addEventListener('mousemove', (e) => {
    if (is_scrolling) {
      const delta_y = e.clientY - start_y;
      scroll_speed = delta_y * 0.2; // Adjust multiplier for sensitivity

      // Update arrow height and direction
      const height = Math.abs(scroll_speed) * 5; // Arrow length scales with speed
      if (scroll_speed > 0) {
        // Downward scroll: arrow grows downward
        arrow.style.top = `${start_y}px`;
        arrow.style.height = `${height}px`;
        arrow.style.backgroundColor = 'red';
      } else {
        // Upward scroll: arrow grows upward
        arrow.style.top = `${start_y + scroll_speed * 5}px`;
        arrow.style.height = `${height}px`;
        arrow.style.backgroundColor = 'blue';
      }
    }
  });

  // Perform scrolling
  function scroll_page() {
    if (is_scrolling) {
      window.scrollBy(0, scroll_speed);
    }
    requestAnimationFrame(scroll_page);
  }

  scroll_page(); // Start the scroll loop
}
