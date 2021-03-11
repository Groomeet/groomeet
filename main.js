const init = async () => {
	const config = await (await fetch('config.json')).json();
	let newHTML = document.documentElement.innerHTML;
	Object.keys(config).map((key) => {
		newHTML = newHTML.replace(key, config[key]);
	});
	document.documentElement.innerHTML = newHTML;
};
init();