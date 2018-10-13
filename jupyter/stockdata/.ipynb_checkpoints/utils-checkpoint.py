
def search_stats_code(code, keyword):
    result = {}
    result['status'] = 'FAIL'
    result['message'] = '잘못된 형식의 데이터입니다.'

    if not type(code) is dict:
        return result

    if not 'StatisticTableList' in code.keys():
        return result

    if not 'row' in code['StatisticTableList'].keys():
        return result

    nameList = map(lambda x: x['STAT_NAME'] if x.get(
        'STAT_NAME') else '', code['StatisticTableList']['row'])
    resultData = []
    for idx, name in enumerate(nameList):
        if name.find(keyword) >= 0:
            resultData.append(code['StatisticTableList']['row'][idx])

    if not resultData:
        result['message'] = '해당 통계를 찾을 수 없습니다.'
        return result
    else:
        result['status'] = "SUCCESS"
        result.pop('message')
        result['data'] = resultData
        return result
