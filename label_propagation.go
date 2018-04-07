package main

import (
    "fmt"
    "os"
    "io"
    "bufio"
    "encoding/csv"
    "gonum.org/v1/gonum/graph/simple"
)

func main() {

}

func buildGraph() *simple.DirectedGraph {
    fmt.Println("Building graph from processed.csv ...")
    data, err := os.Open("processed.csv")
    if err != nil {
        panic(err)
    }

    reader := csv.NewReader(bufio.NewReader(data))
    network := simple.NewDirectedGraph(0, 0)

    // Map for managing node name correspondence with 
    nodeMap := make(map[string]int)
    nm_count := 1

    for {
        connection, err := reader.Read()
        if err == io.EOF {
            break
        } else if err != nil {
            panic(err)
        }

    }
}
