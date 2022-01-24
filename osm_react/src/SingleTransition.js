import React, {useState} from "react";
import {Transition} from "react-transition-group";
import Style from "./singleTransition.module.scss";

//トランジションのスタイル4種類を定義(使わないものは省略可能)
const transitionStyle = {
    entering: {
        transition: "all 1s ease",
        transform: "translateY(220px) ",
        backgroundColor: "red"
    },
    entered: {
        transition: "all 1s ease",
        transform: "translateY(220px) ",
        backgroundColor: "green"
    },
    exiting: {
        transition: "all 1s ease",
        transform: "translateY(0)",
        backgroundColor: "blue",
    },
    exited: {
        transition: "all 1s ease",
        transform: "translateY(0)",
        backgroundColor: "gray",
    },
};

//SingleTransitionコンポーネント
const SingleTransition = () => {

    //マウントの状態を管理
    const [mount, setMount] = useState(false);

    //マウントのオンオフを切り替える
    const changer = () => {
        setMount(!mount);
    };
    
    return (
        <div className={Style.wrapper}>
            <button onClick={changer}>inの切り替え</button>
            <div className={Style.circleGroup}>
                <div className={Style.circleMember}>
                    <Transition in={mount} timeout={1000}>
                        {(state) =>
                            <div className={Style.circleShape} style={transitionStyle[state]}>
                                <div>
                                    <p className={Style.circleText}> {mount ? "in=true" : "in=false"}</p>
                                    <p className={Style.circleText}> {state}</p>
                                </div>
                            </div>}
                    </Transition>
                </div>
            </div>
        </div>
    );
}
export default SingleTransition;