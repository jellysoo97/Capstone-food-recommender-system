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
  const [ratings, setRatings] = useState([])
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
      .post("http://localhost:8000/preference/last", {
        user_id: parseInt(window.localStorage.getItem("sgid")),
        ratings: ratings,
      })
      .then((response) => {
        console.log(response.data)
        window.localStorage.removeItem("sgid")
        alert("회원가입이 완료되었습니다.")
        navigate("/login")
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const saveStar = (e, index) => {
    e.preventDefault()
    let target_value = parseInt(e.target.value)
    console.log(target_value)
    if (e.target.checked) {
      console.log(index, e.target.value)
      for (let i = 1; i < 6; i++) {
        let target_star = document.querySelector(
          "label[for='" + `${index} ${i}-stars` + "']"
        )
        if (i <= target_value) {
          target_star.style.color = "#fc0"
        } else {
          target_star.style.color = "#ccc"
        }
      }
      star[index] = target_value
      setStar(star)
    }
    ratings[index] = {
      recipe_id: menulist[index].recipe_id,
      ratings: target_value,
    }
    setRatings(ratings)
  }

  return (
    <div className="container-fluid d-flex lg-bg">
      <div className="fp-box">
        <div className="lg-title text-center mb-3">초기 선호도 조사</div>
        <div className="text-center mb-2">
          해당 음식에 대한 선호도를 0점부터 5점까지 표시해주세요.
        </div>
        <div className="fp-inner-box overflow-auto">
          {menulist
            ? menulist.map((el, index) => {
                return (
                  <div className="d-flex align-items-center p-3" key={index}>
                    <div className="d-shrink-0 w-50">
                      <img src={el.img_url} />
                    </div>
                    <div className="flex-grow-1 text-center">
                      <h5>{el.recipe_nm_ko}</h5>
                      <div className="star-rating">
                        <input
                          type="radio"
                          id={`${index} 5-stars`}
                          name="rating"
                          value="5"
                          onClick={(e) => saveStar(e, index)}
                        />
                        <label for={`${index} 5-stars`} className="star">
                          &#9733;
                        </label>
                        <input
                          type="radio"
                          id={`${index} 4-stars`}
                          name="rating"
                          value="4"
                          onClick={(e) => saveStar(e, index)}
                        />
                        <label for={`${index} 4-stars`} className="star">
                          &#9733;
                        </label>
                        <input
                          type="radio"
                          id={`${index} 3-stars`}
                          name="rating"
                          value="3"
                          onClick={(e) => saveStar(e, index)}
                        />
                        <label for={`${index} 3-stars`} className="star">
                          &#9733;
                        </label>
                        <input
                          type="radio"
                          id={`${index} 2-stars`}
                          name="rating"
                          value="2"
                          onClick={(e) => saveStar(e, index)}
                        />
                        <label for={`${index} 2-stars`} className="star">
                          &#9733;
                        </label>
                        <input
                          type="radio"
                          id={`${index} 1-stars`}
                          name="rating"
                          value="1"
                          onClick={(e) => saveStar(e, index)}
                        />
                        <label for={`${index} 1-stars`} className="star">
                          &#9733;
                        </label>
                      </div>
                    </div>
                  </div>
                )
              })
            : ""}
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
