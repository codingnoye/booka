<script>
    import { bookSearch, bookSearchKeywords} from '$lib/api'
    import { page } from '$app/stores'
    import SearchBookList from '$lib/components/SearchBookList.svelte';
    let keyword = $page.params.keyword
    let pageNum = 0 

    const bookSearchP = bookSearchKeywords(keyword,pageNum)
    
</script>

<div class='center'>
<div class="container">
    <div class='result'>'#{keyword}' 검색 결과</div>
    <hr style="border: 1px solid #26282B;"/>

    <div class='container'>
        {#await bookSearchP}
            loading...
        {:then books} 
            <SearchBookList books = {books.books}/>
        {/await}
    </div>
</div>
</div>


<style>
    .center{
        justify-content: center;
        display: flex;
    }
    .container{
        width: 39.375rem;
    }
    .result{
        margin: 2.563rem 0 1.5rem 0;
        font-family: 'Pretendard';
        font-style: normal;
        font-weight: 700;
        font-size: 1.313rem;
        line-height: 1.563rem;
        color: #1B1D1F;
    }
    hr{
        margin-bottom: 1.5rem;
    }
    .image{
        width: 8.25rem;
        height: 11.875rem;
        margin-right: 1.5rem;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        /* background-attachment: fixed; */

    }
    .title{
        font-family: 'Pretendard';
        font-style: normal;
        font-weight: 700;
        font-size: 1.063rem;
        line-height: 1.25rem;
        color: #1B1D1F;
    }

    .author{
        font-family: 'Pretendard';
        font-style: normal;
        font-weight: 400;
        font-size: 0.9rem;
        line-height: 1.125rem;
        color: #72787F;
    }
    .keywords{
        /* font-size: 2rem;
        font-weight: 500; */
        margin-top: 1.2rem;
    }
    .keyword{
        display: inline-flex;
        flex-direction: row;
        align-items: flex-start;
        padding: 7px 12px;

        border: 0.5px solid #454C53;
        box-sizing: border-box;
        border-radius: 100px;

        font-family: 'Pretendard';
        font-style: normal;
        font-weight: 400;
        font-size: 12px;
        line-height: 14px;
        text-align: center;
        margin-right: 0.7rem;
    }
    .row{
        display: flex;
        flex-direction: row;
        margin-bottom: 2.25rem;
        /* justify-content: space-between; */
    }
</style>
