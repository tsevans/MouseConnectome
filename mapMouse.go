package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
)

func main() {
	// Open unprocessed csv file
	infile, err := os.Open("dataset03.csv")
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

	var lineCount int
	var skipCount int = 3

	for {
		// Read current row of unprocessed csv
		row, err := reader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err)
		}

		// Skip first four header rows
		if skipCount > 0 {
			skipCount--
			continue
		}

		// Check if connection was selected for article
		if lineCount < 77 {

			// Write relevant values to csv
			pair := make([]string, 2)
			pair[0] = row[4]
			pair[1] = row[3]
			writer.Write(pair)
			fmt.Println(row[4], " --> ", row[3])
			lineCount++
		}
	}

	fmt.Println(lineCount, "lines were written to processed.csv")
}
