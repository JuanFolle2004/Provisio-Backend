<?php

declare(strict_types=1);

namespace Controllers;

use Illuminate\Http\JsonResponse;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\AllowedSort;
use Spatie\QueryBuilder\QueryBuilder;
use Src\Groups\App\Resources\ProductResource;
use Src\Products\Domain\Model\Product;

class ListProductController
{
    public function __invoke(): JsonResponse
    {
        $query = QueryBuilder::for(Product::class)
            ->allowedFilters([
                AllowedFilter::exact('is_free'),
            ])
        ->allowedSorts([
            AllowedSort::field('name'),
            AllowedSort::field('amount'),
        ]);

        return ProductResource::collection($query->paginate(10))->response();
    }
}
