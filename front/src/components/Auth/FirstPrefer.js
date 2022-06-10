import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"

function FirstPrefer() {
  const navigate = useNavigate()
  const [menulist, setMenulist] = useState([])
  const [star, setStar] = useState({
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
  })
  let data_list = []

  useEffect(() => {
    function getMenuList() {
      axios
        .get("http://localhost:8000/preference/first")
        .then((response) => {
          const data = JSON.parse(response.data)
          for (let elem in data) {
            data_list.push({ ...data[elem] })
          }
          setMenulist([...data_list])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getMenuList()
  }, [setMenulist])

  const endSignup = (e) => {
    e.preventDefault()
    axios
      .post("url", {})
      .then((response) => {
        console.log(response.data)
        alert("회원가입이 완료되었습니다.")
        navigate("/login")
      })
      .catch((error) => {
        console.log(error)
      })
  }

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

  const Stars = ({ index }) => {
    return (
      <div className="fp-child visually-hidden" id={`starbox${index}`}>
        <input
          type="radio"
          id="5-stars"
          name="rating"
          value="5"
          onClick={(e) => saveStar(e, index)}
        />
        <label for="5-stars" className="star">
          &#9733;
        </label>
        <input
          type="radio"
          id="4-stars"
          name="rating"
          value="4"
          onClick={(e) => saveStar(e, index)}
        />
        <label for="4-stars" className="star">
          &#9733;
        </label>
        <input
          type="radio"
          id="3-stars"
          name="rating"
          value="3"
          onClick={(e) => saveStar(e, index)}
        />
        <label for="3-stars" className="star">
          &#9733;
        </label>
        <input
          type="radio"
          id="2-stars"
          name="rating"
          value="2"
          onClick={(e) => saveStar(e, index)}
        />
        <label for="2-stars" className="star">
          &#9733;
        </label>
        <input
          type="radio"
          id="1-star"
          name="rating"
          value="1"
          onClick={(e) => saveStar(e, index)}
        />
        <label for="1-star" className="star">
          &#9733;
        </label>
      </div>
    )
  }

  const CarouselItems = ({ src, menu_name, index }) => {
    return (
      <div className="carousel-item parent" data-bs-interval="10000">
        <Stars index={index} />
        <img
          src={src}
          className="d-block w-100"
          alt="..."
          id={`item${index}`}
          onClick={(e) => handleStar(e, index)}
        />
        <div className="carousel-caption d-none d-md-block">
          <h5>{menu_name}</h5>
        </div>
      </div>
    )
  }

  const handleStar = (e, index) => {
    e.preventDefault()
    console.log(index)
    const star_box = document.getElementById(`starbox${index}`)
    if (star_box.classList.contains("visually-hidden")) {
      star_box.classList.remove("visually-hidden")
    } else {
      star_box.classList.add("visually-hidden")
    }
  }

  const saveStar = (e, index) => {
    console.log("imgindex", index)
    e.preventDefault()
    star[index] = 5 - e.target.value
    setStar(star)
  }

  return (
    <div className="container-fluid d-flex lg-bg">
      <div className="fp-box">
        <div className="lg-title text-center mb-3">초기 선호도 조사</div>
        <div className="text-center mb-2">
          음식 사진 클릭 후 해당 음식에 대한 선호도를 0점부터 5점까지
          표시해주세요.
        </div>
        <div
          id="carouselExampleCaptions"
          className="carousel slide"
          data-bs-ride="carousel"
        >
          <div className="carousel-indicators">
            {menulist
              ? menulist.map((el, index) => {
                  if (index == 0) {
                    return (
                      <button
                        type="button"
                        data-bs-target="#carouselExampleCaptions"
                        data-bs-slide-to="0"
                        className="active"
                        aria-current="true"
                        aria-label="Slide 1"
                      ></button>
                    )
                  } else {
                    return (
                      <Indicators slide={index} label={`Slide ${index + 1}`} />
                    )
                  }
                })
              : ""}
          </div>
          <div className="carousel-inner">
            {menulist
              ? menulist.map((el, index) => {
                  if (index == 0) {
                    return (
                      <div className="carousel-item active">
                        <Stars index={index} />
                        <img
                          src={`${menulist[0].img_url}`}
                          className="d-block w-100"
                          alt="..."
                          id="item0"
                          onClick={(e) => handleStar(e, index)}
                        />
                        <div className="carousel-caption d-none d-md-block">
                          <h5>{menulist[0].recipe_nm_ko}</h5>
                        </div>
                      </div>
                    )
                  } else {
                    return (
                      <CarouselItems
                        src={el.img_url}
                        menu_name={el.recipe_nm_ko}
                        index={index}
                      />
                    )
                  }
                })
              : ""}
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
        <div className="d-flex justify-content-center mt-2">
          <button type="button" className="fp-regi" onClick={endSignup}>
            회원가입
          </button>
        </div>
      </div>
    </div>
  )
}

export default FirstPrefer
