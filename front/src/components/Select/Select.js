import React, { useState, useEffect } from "react"
import axios from "axios"

import Table from "./Table/Table.js"

function Select() {
  const [datalist, setDatalist] = useState()

  useEffect(() => {
    function getData() {
      axios
        .get("https://jsonplaceholder.typicode.com/posts")
        .then((response) => {
          console.log(response.data)
          setDatalist([...response.data])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getData()
  }, [])

  return (
    <div>
      <Table datalist={datalist} />
    </div>
  )
}

export default Select
