import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import './card.css'

const useStyles = makeStyles({
    root: {
        maxWidth: 345,
    },
    media: {
        height: 200,
        objectFit: "contain",
    },
    img_contain: {
        maxWidth: '100%',
        maxHeight: '30%',
        padding: '10px',
        // backgroundColor: 'rgba(255,255,255,0.48)',

    },
    align_center: {
        textAlign: "center",
        maxWidth: '30%',
        marginRight: 'auto',
        marginLeft: 'auto',
        // backgroundColor: 'rgba(255,255,255,0.38)'
    },
    typography: {
        fontFamily: 'Shino',
    }

});

function calAttack(props) {
    if (props.progress >= 0) {
        return "GO GO"
    } else {
        return Math.abs(Math.round((props.progress / props.max) * 100)) + '％ Attacked!!'
    }
}

function ackComment(props) {
    if (props.progress == 0) {
        return <div>現状維持！散らかさない！</div>
    } else if (props.progress <= 0) {
        return <div>{props.progress}のダメージ！！</div>
    } else {
        return <div>さぁ片付けましょう！！</div>
    }
}

export default function MediaCard(props) {
    const classes = useStyles();

    return (
        <Card className={classes.root}>
            <CardActionArea>
                {/*<CardMedia*/}
                {/*    className={classes.media}*/}
                {/*    image={props.image}*/}
                {/*    title="Contemplative Reptile"*/}
                {/*/>*/}
                <div className={classes.align_center}>
                    <img className={classes.img_contain} src={props.image} alt="海の写真" title="空と海"></img>
                </div>

                <CardContent>
                    <Typography gutterBottom variant="h5" component="h2">
                        {calAttack(props)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" component="p">
                        {ackComment(props)}
                    </Typography>
                </CardContent>
            </CardActionArea>
            {/*<CardActions>*/}
            {/*    <Button size="small" color="primary">*/}
            {/*        Share*/}
            {/*    </Button>*/}
            {/*    <Button size="small" color="primary">*/}
            {/*        Learn More*/}
            {/*    </Button>*/}
            {/*</CardActions>*/}
        </Card>
    );
}