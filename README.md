# Railroad_Map
Used Google Maps and gRPC to help visualize the benefits of the A* graph search

### Table of Contents
- [Railroad_Map](#railroad-map)
    + [Background](#background)
    + [This Project](#this-project)
    + [Examples](#examples)
    + [Technologies](#technologies)
    + [Running Locally](#running-locally)


### Background
  Graph searching problems are generally phrased as follows: given a graph and two nodes in that graph, what is the shortest path between the two nodes. The canonically famous solution to this problem is [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) which is an adaptation on a breadth first search to include weighted edges. However, Dijkstra's algorithm is not very fast. A variant known as [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) is significantly faster. If you've ever used a GPS to get directions, you can thank A* for the speed.

  So why is A* so much faster? That is the question this visualization seeks to make clear. The difference between A* and Dijkstra is that  Dijkstra's algorithm simply fans out from the source node until it finds the destination. At each step, Dijkstra's algorithm decides what node to look at first based on it's distance from the source node alone. In contrast, A* makes its decisions about what node to inspect based on both the distance traveled from the source node **_and_** a guess about how far that node is from the destination. Imagine you were looking at a map to find the best way from Chicago to Dallas. Would you consider going 100 miles north in the hopes that magically transports you to Dallas? Probably not. As humans, we are smart enough to keep the destination in mind. You know that Dallas is south of Chicago, so generally you would shy away from paths that take you north because it's the opposite direction from where you want to go. So while Dijkstra will generally check paths fanning out in a circular manner, A* will direct itself towards the destination at every step of the way.

  The result: A* outperforms Dijkstra because it reaches the destination faster. It checks fewer paths because it keeps the correct direction in mind at all times.

### This Project
  This project applies these graph searches to a map of railroads spanning the United States. It allows you to select a source city and a destination city, then performs both graph searches. To visualize what paths are checked by each search, it draws the paths on a map using the Google Maps API. Paths drawn in red are those inspected by A*, those in green are those inspected by Dijkstra's algorithm, and the remaining unchecked paths are drawn in blue. This lets us see that A* simply checks fewer paths than Dijkstra, and that while it fans out around the source city at first, it generally becomes more pointed toward the destination as time goes on.

### Examples
  Here is a visualization of the path from Washington, D.C. to Minneapolis:
  ![Sample visualization](screenshots/screenshot.jpg?raw=true "Screenshot of A* Visualization - Washington, D.C. to Minneapolis")
  Chicago to Dallas:
  ![Sample visualization](screenshots/screenshot2.jpg?raw=true "Screenshot of A* Visualization - Chicago to Dallas")
  Chicago to Atlanta:
  ![Sample visualization](screenshots/screenshot3.jpg?raw=true "Screenshot of A* Visualization - Chicago to Atlanta")

### Technologies
- [Flask](http://flask.pocoo.org/): a super lightweight and quick to use web framework for Python.
- [Protocol Buffers](https://developers.google.com/protocol-buffers/): a minimalist serialization tool allowing cross-language and cross-process data structured data transfer with very little memory overhead.
- [gRPC](https://grpc.io/about/): a tool for creating Remote Procedure Call (RPC) services with Protocol Buffers. Generates boilerplate service code which allows clients to communicate to servers running in different threads over HTTP/2.
- [Edward](http://engblog.yext.com/edward/): a tool for managing projects that require multiple services running on different processes.
- [Google Maps API](https://developers.google.com/maps/documentation/javascript/tutorial): Google's JavaScript API to work with embedded maps in websites.

### Running Locally
There are a couple steps to getting the server running locally:
<ol>
	<li>Install the dependencies with <code>pip install -r requirements.txt</code></li>
	<li>
		Get a Google Maps API key from the Google Developer Console and save it into a
		<code>secret.py</code> file similar to the example given. If you just edit the
		example file directly, make sure to remove the example file extension so Python
		can import it correctly.
	</li>
	<li>
		Generate the base gRPC code and Protobuf classes by navigating into the <code>service</code>
		directory and running the build script.
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
