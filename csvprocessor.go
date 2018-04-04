package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
)

func main() {
	// Open unprocessed csv file
	infile, err := os.Open("unprocessed_data.csv")
	if err != nil {
		panic(err)
	}
	defer infile.Close()

	// Create reader for unprocessed csv file
	reader := csv.NewReader(infile)

	// Create new csv for parsed data
	outfile, err := os.Create("processed.csv")
	if err != nil {
		panic(err)
	}
	defer outfile.Close()

	// Create writer for new csv
	writer := csv.NewWriter(outfile)
	defer writer.Flush()

	var lineCount int = 0
	for {
		// Read current row of unprocessed csv
		row, err := reader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err)
		}

		// Write relevant values to new csv
		pair := make([]string, 2)
		pair[0] = row[1]
		pair[1] = row[3]
		writer.Write(pair)
		lineCount++
	}

	fmt.Println(lineCount, "lines written to file.")
}
