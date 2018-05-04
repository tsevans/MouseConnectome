# Mouse Connectome
CS 4984 Computing The Brain Capstone semester project. 

A [recent paper](http://www.pnas.org/content/pnas/114/45/E9692.full.pdf) titled "Organizing principles for the cerebral cortex network of commissural and association connections" has published and analyzed a comprehensive connectome of the mouse brain, collected from findings in over 185 publications that appeared in the literature since 1974. The goal of this project is to analyze the structural properties of this connectome. We are specifically interested in overlapping mudular structure of the networks.

## Background
The current data for the model of a rat's brain consists of two, bilaterally symmetric cortical domains with identical sets of association connections. Each domain has 5,852 (<img src="https://latex.codecogs.com/gif.latex?77^{2}-77" title="77^{2}-77" />) possible association connections and 5,929 commissural connections (<img src="https://latex.codecogs.com/gif.latex?77^{2}" title="77^{2}" />), for a total of 11,740 association connections and 11,858 commissural connections in both domains.

## Datasets
  - mouse_regions.txt
    * Tab delimited list of all 77 regions in the mouse connectome, each line contains the acronym for the region and the full name of the region.
  - final_mouse_weighted.txt
    * Tab delimited edge list of all 154 connections in the mouse cerebral cortex. Each line contains the name of a source node, the name of the corresponding destination node, and the weight for that connection.
