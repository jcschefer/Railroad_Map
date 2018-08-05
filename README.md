# Railroad_Map
Used Google Maps and gRPC to help visualize the benefits of the A* graph search

<h3>Background</h3>
   The A* search is designed to outperform other graph searches by a heuristically guessing the next node in the graph to check. This means that the algorithm will only have to check a fraction of the total paths before finding the shortest solution. As you can see in the example screenshots provided, the A* search(red) ouperforms the Dijkstra's algorithm (green). The blue paths represent all remaining nodes in the tree that neither algorithm checked.

Here is a visualization of the path from Washington, D.C. to Minneapolis:
![Sample visualization](screenshots/screenshot.jpg?raw=true "Screenshot of A* Visualization - Washington, D.C. to Minneapolis")
Chicago to Dallas:
![Sample visualization](screenshots/screenshot2.jpg?raw=true "Screenshot of A* Visualization - Chicago to Dallas")
Chicago to Atlanta:
![Sample visualization](screenshots/screenshot3.jpg?raw=true "Screenshot of A* Visualization - Chicago to Atlanta")

<h3>Running Locally</h3>
There are a couple steps to getting the server running locally:
<ol>
	<li>Install the dependencies with <code>pip install -r requirements.txt</code></li>
	<li>
		Get a Google Maps API key from the Google Developer Console and save it into a
		<code>secret.py</code> file similar to the example given. If you just edit the
		example file directly, make sure to remove the example file extension so Python
		can import it correctly.
	</li>
	<li>Start up the services (web server and backend gRPC server). This can be done one of
		two ways. They can be started separately using <code>python3 server.py</code> and
		<code>python3 service/railroad_server.py</code>. Alternatively, this project is
		configured to use <a href="https://github.com/yext/edward">edward</a> so if you 
		have it installed you can just run <code>edward start web server</code></li>
	<li>
		Fire up your web browser and navigate to <a href="https://localhost:5000">localhost:5000</a>
	</li>
	<li>
		Pick a source and destination from the dropdowns and hit submit to see the results
	</li>
</ol>
