pyPipeline
====================

Open any number of sockets on declared ports and create pipe between them.

Usage
-----
positional arguments:

  N           Ports to open

optional arguments:

  -h, --help  show this help message and exit

  -l          just localports

  -v          increase output verbosity


Example
-------
python pyPipeline.py 1000 1001 -l -v

Open ports 1000 and 1001 on localport. Send message between them. Write verbose to stdout.


python pyPipeline.py 1000 1001 1002

Open ports 1000, 1001 and 1002 on 0.0.0.0. Send message between them.


Author
------
Ignacy Niwald

License
-------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU LESSER GENERAL PUBLIC LICENSE for more details.

You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
along with this program.  If not, see <http://www.gnu.org/licenses/>