from easy_patents.get_info import app_progress
from easy_patents.errors import NoDocumentError, TooManyAccessError


def gene_app_number(year, start, max_count,
        law="trademark", reget_date=1, skip=50, 
        max_no_document_error=30, excludes={'714011053', '302041154'},
        haifun=True):
    '''
    機械的アクセスを行う場合の出願番号を自動生成する関数
    大量出願を行う出願人を除外した出願番号を生成する

    Parameters
    ----------
    year: int
        対象の年の出願
    start: int
        下6桁の開始番号
    max_count: int
        生成する出願番号の最大数
    law: str
        法域
    reget_date: int
        app_progressの再取得日
    skip: int
        excludeの出願人が発見された場合にスキップする件数
    max_no_document_error: int
        連続してNoDocumentErrorになった場合の最大数 
    exclude: set
        生成対象外とする出願人のコード
    haifun: boolean
        生成する出願番号にハイフンを含めるかどうか

    Returns
    -------
    str
        出願番号(10桁の数字の文字列)をyieldする

    Examples
    --------
    >>> for app_number in gene_app_number(year=2020, start=5, max_count=10):
    ...     print(app_number)
    2020-000005
    2020-000006
    2020-000007
    2020-000008
    2020-000209
    2020-000210
    2020-000211
    2020-000212
    2020-000213
    2020-000214
    '''
    count = 0
    num = start
    no_document_error = 0
    while count < max_count:
        if haifun:
            app_number = "%s-%06d" % (year, num)
        else:
            app_number = "%s%06d" % (year, num)
        try:
            progress_info = app_progress(app_number, law, reget_date=reget_date)
            applicant_code = progress_info['result']['data']['applicantAttorney'][0]['applicantAttorneyCd']
            no_document_error = 0
            if applicant_code in excludes:
                num += skip
                continue
            else:
                num += 1
                count += 1
                yield app_number
        except NoDocumentError:
            num += 1
            no_document_error += 1
            if no_document_error > max_no_document_error:
                return
        except TooManyAccessError:
            return
    else:
        return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
