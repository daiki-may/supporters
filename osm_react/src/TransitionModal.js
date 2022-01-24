import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import ImageList from '@material-ui/core/ImageList';
import ImageListItem from '@material-ui/core/ImageListItem';
import './result.css'

var image_url

const useStyles = makeStyles((theme) => ({
    modal: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    paper: {
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
        width: '55%',
        textAlign: 'center'
    },
}));

export default function TransitionsModal(props) {
    const classes = useStyles();
    console.log('props : ', props)
    const [open, setOpen] = React.useState(props.flag);

    const handleOpen = () => {
        console.log('4')
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };


    function getGomi(count) {

        props.storage.child(`gomi_${count}.png`).getDownloadURL().then(function (url) {
            image_url = url;
            return url;
            // console.log('img', url)
        }).catch(function (error) {
            // Handle any errors
        });
        console.log(`gomi_${count}.png`, image_url)
        return image_url
    }

    // //props.count
    //
    // const itemData = [];
    // for (let i = 1; i < 4; i++) {
    //     itemData.push({img: getGomi(i)})
    //     console.log(`gomi_${i}.png`)
    // }

    return (
        <div>
            {console.log(3)}
            <Modal
                aria-labelledby="transition-modal-title"
                aria-describedby="transition-modal-description"
                className={classes.modal}
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                    timeout: 500,
                }}
            >
                <Fade in={open}>
                    <div className={classes.paper}>
                        <h2 id="transition-modal-title">よくできました！</h2>
                        <p id="transition-modal-description">You win!</p>
                        {props.data.map((item) => (
                            <img className={'result'} src={item.img} key={item.key}/>
                        ))}
                    </div>

                </Fade>
            </Modal>
            {console.log(6)}
        </div>
    );
}