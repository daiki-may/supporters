import React, {useState} from 'react';
import {makeStyles, withStyles, lighten} from "@material-ui/core";
import CircularProgress from '@material-ui/core/LinearProgress';
import LinearProgress from '@material-ui/core/LinearProgress';

const ColorCircularProgress = withStyles({
    root: {
        color: '#00695c',
    },
})(CircularProgress);

const ColorLinearProgress = withStyles({
    colorPrimary: {
        backgroundColor: '#b2dfdb',
    },
    barColorPrimary: {
        backgroundColor: '#00695c',
    },
})(LinearProgress);

const BorderLinearProgress = withStyles({
    root: {
        height: 10,
        width: 600,
        backgroundColor: lighten('#ff6c5c', 0.5),
    },
    bar: {
        borderRadius: 20,
        backgroundColor: '#ff6c5c',
    },
})(LinearProgress);

// Inspired by the Facebook spinners.
const useStylesFacebook = makeStyles({
    root: {
        position: 'relative',
    },
    top: {
        color: '#eef3fd',
    },
    bottom: {
        color: '#6798e5',
        animationDuration: '550ms',
        position: 'absolute',
        left: 0,
    },
});

function FacebookProgress(props) {
    const classes = useStylesFacebook();

    return (
        <div className={classes.root}>

        </div>
    );
}

const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
        textAlign: 'center'
    },
    margin: {
        margin: theme.spacing(1),
        width: '60%',
        textAlign: 'center',
        marginLeft: 'auto',
        marginRight: 'auto'
    },
}));


export default function CustomizedProgressBars(props) {
    const classes = useStyles();
    // console.log(props.progress);
    // console.log(props.max);

    return (
        <div className={classes.root}>
            <BorderLinearProgress className={classes.margin} variant="determinate" color="secondary"
                                  value={(props.progress / props.max) * 100}/>
        </div>
    );
}