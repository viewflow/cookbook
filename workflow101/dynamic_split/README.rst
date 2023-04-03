==================
Extending Viewflow
==================

This project demonstrates how to extend Viewflow with custom nodes. The
nodes.DynamicSplit class is an example of a custom dynamic split node that
collects responses from different users and joins them together. The required
number of users is determined in the first step of the process.

http://demo.viewflow.io/workflow/flows/dynamicsplit/

.. image:: doc/DynamicSplit.png
   :width: 400px


Custom Nodes
============

The `nodes.py`_ file contains custom Node classes for this project. The
DynamicSplit class is an example of a custom dynamic split node that collects
responses from different users and joins them together.

Example
=======

To see an example of this project in action, visit
http://demo.viewflow.io/workflow/flows/dynamicsplit/.

