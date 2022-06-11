import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { MultiSelect } from "react-multi-select-component"

import "../../index.css"
import image from "../../images/logo.png"

function Signup() {
  //const url = "https://fad0d70d-d523-442e-8fa3-3fbe1e1b8bf2.mock.pstmn.io/post1"
  const url = "http://localhost:8000/user/account"
  const [data, setData] = useState({
    userid: "",
    userpw: "",
    sex: 1,
    age: 20,
    height: 0,
    weight: 0,
    health: "비활동적",
    isveg: "N",
    vegtype: "N",
    allergic: "N",
  })

  const unableoptions = [
    { label: "메밀", value: "메밀" },
    { label: "밀", value: "밀" },
    { label: "대두", value: "대두" },
    { label: "호두", value: "호두" },
    { label: "땅콩", value: "땅콩" },
    { label: "복숭아", value: "복숭아" },
    { label: "토마토", value: "토마토" },
    { label: "돼지고기", value: "돼지고기" },
    { label: "난류(가금류)", value: "난류" },
    { label: "우유", value: "우유" },
    { label: "닭고기", value: "닭고기" },
    { label: "쇠고기(소고기)", value: "소고기" },
    { label: "새우", value: "새우" },
    { label: "고등어", value: "고등어" },
    { label: "홍합", value: "홍합" },
    { label: "전복", value: "전복" },
    { label: "굴", value: "굴" },
    { label: "조개류", value: "조개류" },
    { label: "게", value: "게" },
    { label: "오징어", value: "오징어" },
    { label: "아황산포함식품", value: ["포도주", "햄", "소시지"] },
  ]
  const [unableselected, setunableSelected] = useState([])
  let newunable = []
  const navigate = useNavigate()

  function submit(e) {
    e.preventDefault()
    if (unableselected.length !== 0) {
      for (let i = 0; i < unableselected.length; i++) {
        if (unableselected[i].label == "아황산포함식품") {
          newunable.push("포도주", "햄", "소시지")
        } else {
          newunable.push(unableselected[i].value)
        }
      }
      console.log(newunable, String(newunable))
    } else {
      newunable = "[]"
    }
    axios
      .post(url, {
        user_id: data.userid,
        password: data.userpw,
        sex: parseInt(data.sex),
        age: parseInt(data.age),
        height: parseFloat(data.height),
        weight: parseFloat(data.weight),
        health: data.health,
        vegtype: data.vegtype,
        allergic: String(newunable),
      })
      .then((res) => {
        console.log(res.data)
        window.localStorage.setItem("sgid", res.data.id)
        navigate("/prefer")
      })
  }

  function handle(e) {
    const newdata = { ...data }
    newdata[e.target.id] = e.target.value
    setData(newdata)
  }

  function changedis(e) {
    if (e.target.value === "Y") {
      if (e.target.id === "isveg") {
        document.getElementById("vegdiv").style.display = "flex"
      } else if (e.target.id === "allergic") {
        document.getElementById("alldiv").style.display = "flex"
      }
    } else if (e.target.value === "N") {
      if (e.target.id === "isveg") {
        document.getElementById("vegdiv").style.display = "none"
      } else if (e.target.id === "allergic") {
        document.getElementById("alldiv").style.display = "none"
      }
    }
  }

  return (
    <div className="su-bg" style={{ background: "#A8BA88" }}>
      <div className="su">
        <div className="d-flex justify-content-center">
          <img src={image} width="45" height="45" />
          <h1>나는 뭐 먹지</h1>
        </div>
        <form onSubmit={(e) => submit(e)}>
          <div class="d-flex justify-content-center">
            <label className="su-label">
              <span>아이디</span>
              <input
                onChange={(e) => handle(e)}
                id="userid"
                value={data.userid}
                type="text"
                style={{ width: 320 }}
              />
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>비밀번호</span>
              <input
                onChange={(e) => handle(e)}
                id="userpw"
                value={data.userpw}
                type="password"
                style={{ width: 320 }}
              />
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>성별</span>
              <select
                onChange={(e) => handle(e)}
                id="sex"
                value={data.sex}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="1">남자</option>
                <option value="0">여자</option>
              </select>
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>나이</span>
              <select
                onChange={(e) => handle(e)}
                id="age"
                value={data.age}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="10">10대</option>
                <option value="20">20대</option>
                <option value="30">30대</option>
                <option value="40">40대</option>
                <option value="50">50대</option>
                <option value="60">60대</option>
                <option value="70">70대</option>
                <option value="80">80대</option>
                <option value="90">90대</option>
              </select>
            </label>
          </div>

          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>
                신장을 입력해주세요
                <br />
                &#40;단위 cm&#41;
              </span>
              <input
                onChange={(e) => handle(e)}
                id="height"
                value={data.height}
                style={{ width: 320, textAlign: "center" }}
                type="number"
              />
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>
                체중을 입력해주세요
                <br />
                &#40;단위 kg&#41;
              </span>
              <input
                onChange={(e) => handle(e)}
                id="weight"
                value={data.weight}
                style={{ width: 320, textAlign: "center" }}
                type="number"
              />
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>평소에 활동적이신가요?</span>
              <select
                onChange={(e) => handle(e)}
                id="health"
                value={data.health}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="비활동적">비활동적</option>
                <option value="저활동적">저활동적</option>
                <option value="활동적">활동적</option>
                <option value="매우활동적">매우활동적</option>
              </select>
            </label>
          </div>

          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>채식주의자이신가요?</span>
              <select
                onChange={(e) => {
                  handle(e)
                  changedis(e)
                }}
                id="isveg"
                value={data.isveg}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="Y">네</option>
                <option value="N">아니오</option>
              </select>
            </label>
          </div>
          <div
            id="vegdiv"
            className="justify-content-center"
            style={{ display: "none" }}
          >
            <label className="su-label">
              <span>어느 채식 유형에 속하시나요?</span>
              <select
                onChange={(e) => handle(e)}
                id="vegtype"
                value={data.vegtype}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="N"></option>
                <option value="vegan">비건(vegan)</option>
                <option value="lacto-vegetarian">
                  락토 베지테리언(lacto-vegetarian)
                </option>
                <option value="ovo-vegetarian">
                  오보 베지테리언(ovo-vegetarian)
                </option>
                <option value="lacto-ovo-vegetarian">
                  락토오보 베지테리언(lacto-ovo-vegetarian)
                </option>
                <option value="pesco-vegetarian">
                  페스코 베지테리언(pesco-vegetarian)
                </option>
                <option value="pollo-vegetarian">
                  폴로 베지테리언(pollo-vegetarian)
                </option>
              </select>
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <label className="su-label">
              <span>알레르기가 있으신가요?</span>
              <select
                onChange={(e) => {
                  handle(e)
                  changedis(e)
                }}
                id="allergic"
                value={data.allergic}
                style={{ width: 320, textAlign: "center" }}
              >
                <option value="Y">네</option>
                <option value="N">아니오</option>
              </select>
            </label>
          </div>
          <div
            id="alldiv"
            className="justify-content-center"
            style={{ display: "none" }}
          >
            <label className="su-label2">
              주의해야할 알레르기 성분에 체크해 주세요
              <MultiSelect
                options={unableoptions}
                value={unableselected}
                onChange={setunableSelected}
                labelledBy="Select"
              />
            </label>
          </div>
          <div className="d-flex justify-content-center">
            <button className="su-btn" class="btn btn-outline-dark">
              다음 페이지
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
export default Signup
