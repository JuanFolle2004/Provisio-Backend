<?php

declare(strict_types=1);

namespace Src\Products\App\Controllers;

use Illuminate\Http\JsonResponse;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\AllowedSort;
use Spatie\QueryBuilder\QueryBuilder;

use Src\Groups\Domain\Model\Group;
use Src\Products\App\Resources\ProductResource;
use Src\Products\Domain\Model\Product;

class ListProductController
{
    public function __invoke(Group $group): JsonResponse
    {
        $query = QueryBuilder::for(Product::class)
            ->where('group_id', $group->id)
            ->with('assignments')
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
