import React, { useState, useEffect } from "react"
import axios from "axios"

function FirstPrefer() {
  const [menulist, setMenulist] = useState([])

  useEffect(() => {
    function getMenuList() {
      axios
        .get("http://localhost:8000/")
        .then((response) => {
          console.log(response.data)
          setMenulist(response.data)
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getMenuList()
  }, [])

  const Indicators = ({ slide, label }) => {
    return (
      <button
        type="button"
        data-bs-target="#carouselExampleCaptions"
        data-bs-slide-to={slide}
        aria-label={label}
      ></button>
    )
  }

  const CarouselItems = ({ src, menu_name }) => {
    return (
      <div className="carousel-item active">
        <img src={src} className="d-block w-100" alt="..." />
        <div className="carousel-caption d-none d-md-block">
          <h5>{menu_name}</h5>
        </div>
      </div>
    )
  }

  return (
    <div className="container-fluid d-flex lg-bg">
      <div className="lg-box">
        <div className="lg-title text-center mb-5">초기 선호도 조사</div>
        <div>해당 음식에 대한 선호도를 0점부터 5점까지 표시해주세요.</div>
        <div
          id="carouselExampleCaptions"
          className="carousel slide"
          data-bs-ride="carousel"
        >
          <div className="carousel-indicators">
            <button
              type="button"
              data-bs-target="#carouselExampleCaptions"
              data-bs-slide-to="0"
              className="active"
              aria-current="true"
              aria-label="Slide 1"
            ></button>
            {menulist.map((index) => {
              index < 9 ? (
                <Indicators slide={index + 1} label={`Slide ${index + 2}`} />
              ) : (
                ""
              )
            })}
          </div>
          <div className="carousel-inner">
            {menulist.map((el) => {
              ;<CarouselItems src={el.url} menu_name={el.menu} />
            })}
          </div>
          <button
            className="carousel-control-prev"
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide="prev"
          >
            <span
              className="carousel-control-prev-icon"
              aria-hidden="true"
            ></span>
            <span className="visually-hidden">Previous</span>
          </button>
          <button
            className="carousel-control-next"
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide="next"
          >
            <span
              className="carousel-control-next-icon"
              aria-hidden="true"
            ></span>
            <span className="visually-hidden">Next</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default FirstPrefer
