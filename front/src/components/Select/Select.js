import React, { useState, useEffect } from "react"
import axios from "axios"

import Table from "./Table/Table.js"

function Select() {
  const [group, setGroup] = useState()
  const [ingre, setIngre] = useState()

  useEffect(() => {
    function getData() {
      axios
        .get("https://jsonplaceholder.typicode.com/users")
        .then((response) => {
          setGroup([...response.data[0]])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getData()
  }, [])

  return (
    <div>
      <Table group={group} />
    </div>
  )
}

export default Select
