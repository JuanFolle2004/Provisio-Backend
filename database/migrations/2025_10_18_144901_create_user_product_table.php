<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('assignment', function (Blueprint $table) {
            $table->id();
            $table->foreignId("user_id")->constrained("users");
            $table->foreignId('group_id')->constrained("groups");
            $table->foreignId("product_id")->constrained("products");
            $table->integer('amount');
            $table->integer('bought');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('assignment');
    }
};
