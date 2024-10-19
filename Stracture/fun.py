
def groupingTime(df):
    dff  = df.to_dict('records')
    times = [{'time':x['time'], 'reserve':x['reserve']} for x in dff]
    df = df[df.index==df.index.min()]
    df['time'] = [times]
    df = df[['time']]
    return df

def groupingTimeNoReserve(df):
    times = df['time'].to_list()
    df = df[df.index==df.index.min()]
    df['time'] = [times]
    df = df[['time']]
    return df