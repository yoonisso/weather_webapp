const resizeObserver = new ResizeObserver(entries => {
	entries.forEach(entry => {
		document.querySelector (".image_container").innerHTML = `width: ${entry.contentRect.width} height: ${entry.contentRect.height}`;
	});
});

const elems = document.querySelector('.image_container');
myObserver.observe(elems);

function outputUpdate(radius) {
    document.querySelector('#selected_radius').value = radius + " km";
}